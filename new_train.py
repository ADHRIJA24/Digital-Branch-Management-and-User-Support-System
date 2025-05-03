from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten, MaxPooling1D, BatchNormalization, Dropout
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt

def one_hot_from_item(item, labels):
    """Convert an item (0 or 1) into one-hot encoded format"""
    one_hot = np.zeros(len(labels))
    one_hot[int(item)] = 1
    return one_hot

def plot_training_history(history):
    """Plot training & validation accuracy and loss"""
    plt.figure(figsize=(12, 4))
    
    # Plot training & validation accuracy values
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    
    
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    # Plot training & validation loss values
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()
    plt.close()

def create_and_train_model(X_train, X_test, y_train, y_test):
    """Create and train the CNN model"""
    model = Sequential([
        Conv1D(filters=32, kernel_size=2, activation='relu', padding='same', 
               input_shape=(8, 1)),
        BatchNormalization(),
        Flatten(),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        Dense(2, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Add callbacks
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001
    )
    
    # Train model
    history = model.fit(
        X_train, 
        y_train,
        epochs=30,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping, reduce_lr]
    )
    
    return model, history

def main():
    # Load and prepare data
    df = pd.read_csv(r'C:\Users\DELL\Desktop\project\train.csv', header=None)
    data = np.array(df)
    
    # Split features and labels
    X = data[:, :-1]  # First 8 columns
    y = data[:, -1:]  # Last column
    
    # One-hot encode labels
    y = np.array([one_hot_from_item(item, [0, 1]) for item in y])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Reshape data for Conv1D
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    
    # Create and train model
    model, history = create_and_train_model(X_train, X_test, y_train, y_test)
    
    # Plot training history
    plot_training_history(history)
    
    # Save model
    model_json = model.to_json()
    with open("static/model1.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("static/model1.h5")
    
    # Evaluate model
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)
    
    # Print results
    conf_matrix = confusion_matrix(y_test_classes, y_pred_classes)
    print("\nConfusion Matrix:")
    print(conf_matrix)
    
    accuracy = (y_pred_classes == y_test_classes).mean()
    print(f"\nTest Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()



# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Conv1D, Flatten, BatchNormalization, Dropout
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix
# import pandas as pd
# import matplotlib.pyplot as plt

# # Ensure TensorFlow version
# print(f"TensorFlow version: {tf.__version__}")

# def one_hot_from_item(item, labels):
#     """Convert an item (0 or 1) into one-hot encoded format"""
#     one_hot = np.zeros(len(labels))
#     one_hot[int(item)] = 1
#     return one_hot

# def plot_training_history(history):
#     """Plot training & validation accuracy and loss"""
#     plt.figure(figsize=(12, 4))
    
#     plt.subplot(1, 2, 1)
#     plt.plot(history.history['accuracy'])
#     plt.plot(history.history['val_accuracy'])
#     plt.title('Model accuracy')
#     plt.ylabel('Accuracy')
#     plt.xlabel('Epoch')
#     plt.legend(['Train', 'Validation'], loc='upper left')
    
#     plt.subplot(1, 2, 2)
#     plt.plot(history.history['loss'])
#     plt.plot(history.history['val_loss'])
#     plt.title('Model loss')
#     plt.ylabel('Loss')
#     plt.xlabel('Epoch')
#     plt.legend(['Train', 'Validation'], loc='upper left')
    
#     plt.tight_layout()
#     plt.savefig('training_history.png')
#     plt.show()
#     plt.close()

# def create_and_train_model(X_train, X_test, y_train, y_test):
#     """Create and train the CNN model"""
#     model = Sequential([
#         Conv1D(filters=32, kernel_size=2, activation='relu', padding='same', 
#                input_shape=(8, 1)),
#         BatchNormalization(),
#         Flatten(),
#         Dense(64, activation='relu'),
#         BatchNormalization(),
#         Dropout(0.3),
#         Dense(32, activation='relu'),
#         BatchNormalization(),
#         Dropout(0.2),
#         Dense(2, activation='softmax')
#     ])
    
#     model.compile(
#         optimizer='adam',
#         loss='categorical_crossentropy',
#         metrics=['accuracy']
#     )
    
#     early_stopping = tf.keras.callbacks.EarlyStopping(
#         monitor='val_loss',
#         patience=5,
#         restore_best_weights=True
#     )
    
#     reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
#         monitor='val_loss',
#         factor=0.2,
#         patience=3,
#         min_lr=0.00001
#     )
    
#     history = model.fit(
#         X_train, 
#         y_train,
#         epochs=30,
#         batch_size=32,
#         validation_data=(X_test, y_test),
#         callbacks=[early_stopping, reduce_lr]
#     )
    
#     return model, history

# def main():
#     # Load and prepare data
#     df = pd.read_csv(r'C:\Users\Arya\Desktop\dos train\dos train\train.csv', header=None)
#     data = np.array(df)
    
#     X = data[:, :-1]  # First 8 columns
#     y = data[:, -1:]  # Last column
    
#     y = np.array([one_hot_from_item(item, [0, 1]) for item in y])
    
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
#     X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    
#     # Create and train model
#     model, history = create_and_train_model(X_train, X_test, y_train, y_test)
    
#     plot_training_history(history)
    
#     # Save model in .keras format
#     model.save(r"C:\Users\Arya\Desktop\project\static\model1.keras")
    
#     # Evaluate model
#     y_pred = model.predict(X_test)
#     y_pred_classes = np.argmax(y_pred, axis=1)
#     y_test_classes = np.argmax(y_test, axis=1)
    
#     print("\nConfusion Matrix:")
#     print(confusion_matrix(y_test_classes, y_pred_classes))
    
#     accuracy = (y_pred_classes == y_test_classes).mean()
#     print(f"\nTest Accuracy: {accuracy:.4f}")

# if __name__ == "__main__":
#     main()